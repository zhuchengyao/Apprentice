from manim import *
import numpy as np


class NGramLanguageModelExample(Scene):
    """
    Simple n-gram language model: P(w_n | w_{n-1}, w_{n-2}) via
    counts from a training corpus. Demonstrates how bigrams and
    trigrams capture local language structure (before transformers).

    SINGLE_FOCUS:
      Small corpus of 3 sentences, build unigram, bigram, trigram
      counts; ValueTracker n_gram_tr steps n = 1, 2, 3; always_redraw
      bar chart of P(next token) given the last n-1 tokens.
    """

    def construct(self):
        title = Tex(r"$n$-gram model: $P(w_n \mid w_{n-1}, \dots, w_{n-k+1})$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        sentences = [
            ["the", "cat", "sat", "on", "the", "mat"],
            ["the", "dog", "sat", "on", "the", "floor"],
            ["the", "cat", "ate", "the", "fish"],
        ]
        all_tokens = [tok for s in sentences for tok in s]
        vocab = sorted(set(all_tokens))
        V = len(vocab)

        # Count unigrams, bigrams, trigrams
        def unigram_probs():
            counts = {w: 0 for w in vocab}
            for s in sentences:
                for w in s:
                    counts[w] += 1
            total = sum(counts.values())
            return {w: counts[w] / total for w in vocab}

        def bigram_probs_after(prev):
            counts = {w: 0 for w in vocab}
            for s in sentences:
                for i in range(len(s) - 1):
                    if s[i] == prev:
                        counts[s[i + 1]] += 1
            total = sum(counts.values())
            if total == 0:
                return {w: 0 for w in vocab}
            return {w: counts[w] / total for w in vocab}

        def trigram_probs_after(prev2, prev1):
            counts = {w: 0 for w in vocab}
            for s in sentences:
                for i in range(len(s) - 2):
                    if s[i] == prev2 and s[i + 1] == prev1:
                        counts[s[i + 2]] += 1
            total = sum(counts.values())
            if total == 0:
                return {w: 0 for w in vocab}
            return {w: counts[w] / total for w in vocab}

        # Display corpus at top
        corpus_text = VGroup()
        for s in sentences:
            corpus_text.add(Tex(" ".join(s), font_size=18, color=GREY_B))
        corpus_text.arrange(DOWN, aligned_edge=LEFT, buff=0.12
                              ).to_edge(LEFT, buff=0.5).shift(UP * 1.8)
        self.play(Write(corpus_text))

        # Context
        context_lbl = Tex(r"query: after ``the cat''",
                           color=YELLOW, font_size=22).move_to([1.5, 1.8, 0])
        self.play(Write(context_lbl))

        n_gram_tr = ValueTracker(1)

        def probs_now():
            n = int(round(n_gram_tr.get_value()))
            if n == 1:
                return unigram_probs(), "1-gram (prior)"
            elif n == 2:
                return bigram_probs_after("cat"), "2-gram | cat"
            else:
                return trigram_probs_after("the", "cat"), "3-gram | the cat"

        def bar_chart():
            probs, _ = probs_now()
            grp = VGroup()
            x0 = -5
            y0 = -1.5
            for i, w in enumerate(vocab):
                p = probs[w]
                if p < 0.001:
                    continue
                w_bar = p * 6
                bar = Rectangle(width=w_bar, height=0.3,
                                 color=BLUE, fill_opacity=0.65,
                                 stroke_width=1)
                bar.move_to([x0 + w_bar / 2, y0 - i * 0.35, 0])
                grp.add(bar)
                lbl = Tex(w, font_size=14, color=WHITE).next_to(
                    bar, LEFT, buff=0.1)
                grp.add(lbl)
                plbl = MathTex(rf"{p:.2f}", font_size=14,
                                 color=WHITE).next_to(bar, RIGHT, buff=0.08)
                grp.add(plbl)
            return grp

        self.add(always_redraw(bar_chart))

        def method_lbl():
            _, name = probs_now()
            return Tex(name, color=ORANGE, font_size=24
                        ).move_to([3.5, 0.0, 0])

        self.add(always_redraw(method_lbl))

        for target in [2, 3, 1]:
            self.play(n_gram_tr.animate.set_value(target),
                       run_time=1.3, rate_func=smooth)
            self.wait(1.0)
        self.wait(0.4)
