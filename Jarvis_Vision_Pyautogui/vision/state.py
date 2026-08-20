class ScreenState:

    def __init__(
        self,
        summary="",
        errors=None,
        important="",
        task_complete=False,
        confidence=0.0
    ):

        self.summary = summary

        self.errors = (
            errors
            if errors is not None
            else []
        )

        self.important = important

        self.task_complete = task_complete

        self.confidence = confidence


    # ==========================
    # CREATE FROM VISION JSON
    # ==========================

    @classmethod
    def from_json(cls, data):

        return cls(

            summary=data.get(
                "summary",
                ""
            ),

            errors=data.get(
                "errors",
                []
            ),

            important=data.get(
                "important",
                ""
            ),

            task_complete=data.get(
                "task_complete",
                False
            ),

            confidence=data.get(
                "confidence",
                0.0
            )
        )


    # ==========================
    # CONVERT BACK TO DICT
    # ==========================

    def to_dict(self):

        return {

            "summary": self.summary,

            "errors": self.errors,

            "important": self.important,

            "task_complete": self.task_complete,

            "confidence": self.confidence

        }


    # ==========================
    # DEBUG DISPLAY
    # ==========================

    def __str__(self):

        return (
            f"\nSCREEN STATE\n"
            f"-------------\n"
            f"Summary: {self.summary}\n"
            f"Errors: {self.errors}\n"
            f"Important: {self.important}\n"
            f"Complete: {self.task_complete}\n"
            f"Confidence: {self.confidence}\n"
        )