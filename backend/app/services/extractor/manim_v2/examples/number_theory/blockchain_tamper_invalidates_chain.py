from manim import *
import hashlib


class BlockchainTamperInvalidatesChain(Scene):
    """A blockchain is a linked list of blocks where each block's header
    contains the SHA-256 hash of the previous block.  Tamper with one
    block's data and its hash changes.  That hash sits in the next
    block's header, so the next block's hash changes too, cascading
    forward — every downstream block is marked invalid."""

    def construct(self):
        title = Tex(
            r"Tampering one block invalidates the entire downstream chain",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        contents = ["TX: A->B 5", "TX: B->C 2", "TX: C->A 1", "TX: A->D 3"]

        def short_hash(s):
            return hashlib.sha256(s.encode()).hexdigest()[:10]

        prev_hash = "genesis   "
        rows = []
        for content in contents:
            block_payload = prev_hash + "||" + content
            h = short_hash(block_payload)
            rows.append({"prev": prev_hash, "content": content,
                         "hash": h, "orig_hash": h})
            prev_hash = h

        blocks = VGroup()
        block_refs = []
        for i, row in enumerate(rows):
            x = -5.4 + i * 3.4
            body = VGroup(
                Tex("block %d" % (i + 1), font_size=22,
                    color=YELLOW),
                Tex(rf"prev: \texttt{{{row['prev']}}}",
                    font_size=18, color=BLUE),
                Tex(rf"data: \texttt{{{row['content']}}}",
                    font_size=20, color=WHITE),
                Tex(rf"hash: \texttt{{{row['hash']}}}",
                    font_size=18, color=GREEN),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            box = SurroundingRectangle(body, color=GREEN,
                                       buff=0.2, stroke_width=2)
            group = VGroup(box, body).move_to([x, 0.2, 0])
            blocks.add(group)
            block_refs.append({"body": body, "box": box, "row": row})

        self.play(LaggedStart(*[FadeIn(b) for b in blocks],
                              lag_ratio=0.15, run_time=2))

        arrows = VGroup(*[
            Arrow(
                blocks[i].get_right(), blocks[i + 1].get_left(),
                buff=0.1, color=GREY_B, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.1,
            )
            for i in range(len(blocks) - 1)
        ])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                              lag_ratio=0.2))

        cap = Tex(
            r"Tamper with block 2: change data \texttt{B-$>$C 2} $\to$ \texttt{B-$>$E 99}",
            font_size=24, color=RED,
        ).to_edge(DOWN, buff=1.7)
        self.play(FadeIn(cap))

        new_content = "TX: B->E 99"
        block_refs[1]["row"]["content"] = new_content
        new_data = Tex(
            rf"data: \texttt{{{new_content}}}",
            font_size=20, color=RED,
        ).move_to(block_refs[1]["body"][2], aligned_edge=LEFT)
        self.play(Transform(block_refs[1]["body"][2], new_data))

        prev = block_refs[0]["row"]["hash"]
        for i in range(1, len(block_refs)):
            r = block_refs[i]["row"]
            new_hash = short_hash(prev + "||" + r["content"])
            r["hash"] = new_hash
            hash_tex = block_refs[i]["body"][3]
            new_hash_tex = Tex(
                rf"hash: \texttt{{{new_hash}}}",
                font_size=18, color=RED,
            ).move_to(hash_tex, aligned_edge=LEFT)
            new_box = SurroundingRectangle(
                block_refs[i]["body"], color=RED,
                buff=0.2, stroke_width=2.5,
            )
            self.play(
                Transform(hash_tex, new_hash_tex),
                Transform(block_refs[i]["box"], new_box),
                run_time=0.6,
            )
            if i + 1 < len(block_refs):
                prev_tex = block_refs[i + 1]["body"][1]
                new_prev_tex = Tex(
                    rf"prev: \texttt{{{new_hash}}}",
                    font_size=18, color=RED,
                ).move_to(prev_tex, aligned_edge=LEFT)
                self.play(Transform(prev_tex, new_prev_tex), run_time=0.4)
            prev = new_hash

        verdict = Tex(
            r"Every downstream block is invalidated — tampering is caught.",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(verdict))
        self.wait(1.5)
