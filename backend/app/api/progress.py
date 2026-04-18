"""Dashboard & progress API endpoints."""

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import case, func, literal_column, select

from app.database import execute_parallel
from app.dependencies import get_current_user
from app.models.book import Book, BookStatus, Chapter, Section, KnowledgePoint
from app.models.tutor import TutorConversation, TutorMessage
from app.models.user import User, UserStreak

router = APIRouter()


@router.get("/overview")
async def get_overview(
    current_user: User = Depends(get_current_user),
):
    """Dashboard stats: books, KPs, mastery, conversations, streaks."""
    uid = current_user.id
    since = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=30)
    day_col = func.date_trunc(literal_column("'day'"), KnowledgePoint.mastered_at)

    stmts = [
        # books
        select(
            func.count(Book.id).label("total"),
            func.count(case((Book.status == BookStatus.ready, Book.id))).label("ready"),
        ).where(Book.user_id == uid),
        # kp totals
        select(
            func.count(KnowledgePoint.id).label("total"),
            func.count(KnowledgePoint.mastered_at).label("mastered"),
        )
        .select_from(KnowledgePoint)
        .join(Section, Section.id == KnowledgePoint.section_id)
        .join(Chapter, Chapter.id == Section.chapter_id)
        .join(Book, Book.id == Chapter.book_id)
        .where(Book.user_id == uid),
        # per-book breakdown
        select(
            Book.id,
            Book.title,
            Book.status,
            Book.total_pages,
            Book.created_at,
            func.count(KnowledgePoint.id).label("total_kps"),
            func.count(KnowledgePoint.mastered_at).label("mastered_kps"),
        )
        .outerjoin(Chapter, Chapter.book_id == Book.id)
        .outerjoin(Section, Section.chapter_id == Chapter.id)
        .outerjoin(KnowledgePoint, KnowledgePoint.section_id == Section.id)
        .where(Book.user_id == uid)
        .group_by(Book.id, Book.title, Book.status, Book.total_pages, Book.created_at)
        .order_by(Book.created_at.desc()),
        # conversation count
        select(func.count(TutorConversation.id)).where(TutorConversation.user_id == uid),
        # message count
        select(func.count(TutorMessage.id))
        .join(TutorConversation, TutorConversation.id == TutorMessage.conversation_id)
        .where(TutorConversation.user_id == uid),
        # recent conversations
        select(
            TutorConversation.id,
            TutorConversation.updated_at,
            Book.title.label("book_title"),
            Chapter.title.label("chapter_title"),
            func.count(TutorMessage.id).label("message_count"),
        )
        .join(Book, Book.id == TutorConversation.book_id)
        .join(Chapter, Chapter.id == TutorConversation.chapter_id)
        .outerjoin(TutorMessage, TutorMessage.conversation_id == TutorConversation.id)
        .where(TutorConversation.user_id == uid)
        .group_by(TutorConversation.id, TutorConversation.updated_at, Book.title, Chapter.title)
        .order_by(TutorConversation.updated_at.desc())
        .limit(5),
        # streaks (last 30 days)
        select(UserStreak)
        .where(UserStreak.user_id == uid, UserStreak.date >= since.date())
        .order_by(UserStreak.date.desc()),
        # mastery timeline (last 30 days)
        select(day_col.label("day"), func.count(KnowledgePoint.id).label("count"))
        .join(Section, Section.id == KnowledgePoint.section_id)
        .join(Chapter, Chapter.id == Section.chapter_id)
        .join(Book, Book.id == Chapter.book_id)
        .where(
            Book.user_id == uid,
            KnowledgePoint.mastered_at.isnot(None),
            KnowledgePoint.mastered_at >= since,
        )
        .group_by(day_col)
        .order_by(day_col),
    ]

    (
        book_result, kp_result, per_book_result,
        conv_result, msg_result, recent_conv_result,
        streak_result, mastery_timeline_result,
    ) = await execute_parallel(*stmts)

    book_row = book_result.one()
    kp_row = kp_result.one()
    total_kps = int(kp_row.total or 0)
    mastered_kps = int(kp_row.mastered or 0)

    books = []
    for row in per_book_result.all():
        t = int(row.total_kps or 0)
        m = int(row.mastered_kps or 0)
        books.append({
            "id": str(row.id),
            "title": row.title,
            "status": row.status.value if row.status else "unknown",
            "total_pages": row.total_pages,
            "total_kps": t,
            "mastered_kps": m,
            "progress": round(m / t, 3) if t > 0 else 0.0,
        })

    total_conversations = conv_result.scalar() or 0
    total_messages = msg_result.scalar() or 0

    recent_conversations = [
        {
            "id": str(row.id),
            "book_title": row.book_title,
            "chapter_title": row.chapter_title,
            "message_count": int(row.message_count or 0),
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }
        for row in recent_conv_result.all()
    ]

    streaks = streak_result.scalars().all()
    today = datetime.now(UTC).date()
    streak_dates = {s.date for s in streaks}
    current_streak = 0
    check_date = today
    while check_date in streak_dates:
        current_streak += 1
        check_date -= timedelta(days=1)
    # Today not yet logged — count the run ending yesterday instead
    if current_streak == 0:
        check_date = today - timedelta(days=1)
        while check_date in streak_dates:
            current_streak += 1
            check_date -= timedelta(days=1)

    total_study_minutes = sum(s.minutes_studied for s in streaks)
    streak_data = [
        {
            "date": s.date.isoformat(),
            "minutes_studied": s.minutes_studied,
            "points_mastered": s.points_mastered,
        }
        for s in reversed(streaks)
    ]

    mastery_timeline = [
        {
            "date": row.day.strftime("%Y-%m-%d"),
            "points_mastered": int(row.count or 0),
        }
        for row in mastery_timeline_result.all()
    ]

    return {
        "books": {
            "total": int(book_row.total or 0),
            "ready": int(book_row.ready or 0),
            "list": books,
        },
        "knowledge_points": {
            "total": total_kps,
            "mastered": mastered_kps,
            "progress": round(mastered_kps / total_kps, 3) if total_kps > 0 else 0.0,
            "mastery_timeline": mastery_timeline,
        },
        "tutor": {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "recent_conversations": recent_conversations,
        },
        "streaks": {
            "current_streak": current_streak,
            "total_study_minutes": total_study_minutes,
            "daily": streak_data,
        },
    }
