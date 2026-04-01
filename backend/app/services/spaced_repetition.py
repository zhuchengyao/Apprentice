from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SM2Result:
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review_at: datetime


def sm2_algorithm(
    quality: int,
    repetitions: int,
    ease_factor: float,
    interval_days: int,
) -> SM2Result:
    """
    SM-2 spaced repetition algorithm.
    quality: 0 (complete blackout) to 5 (perfect response)
    """
    quality = max(0, min(5, quality))

    if quality >= 3:
        if repetitions == 0:
            interval_days = 1
        elif repetitions == 1:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)
        repetitions += 1
    else:
        repetitions = 0
        interval_days = 1

    ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease_factor = max(1.3, ease_factor)

    next_review = datetime.utcnow() + timedelta(days=interval_days)

    return SM2Result(
        ease_factor=ease_factor,
        interval_days=interval_days,
        repetitions=repetitions,
        next_review_at=next_review,
    )
