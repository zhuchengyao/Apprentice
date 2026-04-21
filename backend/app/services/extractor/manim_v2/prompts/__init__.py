"""Prompt builders for the Manim v2 pipeline. Each module exports a
`build_system_blocks()` + `build_user_message()` pair so callers have a
uniform shape. Keep the system text byte-stable for prompt caching.
"""
