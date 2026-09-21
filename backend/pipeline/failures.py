"""
Pipeline "explicit failure" exceptions.

Principle: LLM unavailable, missing subtitles, empty outline / scores, clips with no
output files — all of these must put the project into a failed state, with the stage
and one actionable user-facing hint; they must not be swallowed and continue into a
`Completed with 0 clips` result (#100 #11 #24 share this symptom).
"""

from __future__ import annotations


class PipelineFailure(RuntimeError):
    """Pipeline failure carrying a stage and a user hint.

    stage: matches the simple_progress stage names (INGEST / SUBTITLE / ANALYZE / HIGHLIGHT / EXPORT),
           surfaced with the frontend failure state and in-app feedback.
    hint:  what the user can do next (which settings page, what to install), appended after the message.
    """

    def __init__(self, stage: str, message: str, hint: str = ""):
        super().__init__(message)
        self.stage = stage
        self.hint = hint

    @property
    def message(self) -> str:
        return str(self.args[0]) if self.args else ""

    def user_message(self) -> str:
        return f"{self.message} {self.hint}".strip()


HINT_CHECK_LLM = "Go to Settings > Model to check the provider, API key, and model name, click Test Connection, then retry."
HINT_SUBTITLE = "Go to Settings > Transcription to install a Whisper model for automatic transcription, or import an .srt subtitle file and retry."
HINT_LOWER_THRESHOLD = "Lower the minimum score threshold under Settings > Model and retry, or switch to a stronger model."
HINT_CHECK_FFMPEG = "Make sure ffmpeg is available (bundled in the desktop build; check PATH for Docker / script mode) and that the source video file is complete and playable."
