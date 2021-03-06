import re

import badges
from badge_triggers import BadgeTriggerType
import discussion.discussion_models


@badges.active_badge
class FirstFlagBadge(badges.Badge):

    def __init__(self):
        badges.Badge.__init__(self)
        self.description = "Markeer Verplichting"
        self.badge_category = badges.BadgeCategory.BRONZE
        self.points = 0

    def extended_description(self):
        return ("Markeer je eerste vraag of plaats een opmerkinge onder een video")

    def is_manually_awarded(self):
        return True


@badges.active_badge
class FirstUpVoteBadge(badges.Badge):

    def __init__(self):
        badges.Badge.__init__(self)
        self.description = "Duimen op"
        self.badge_category = badges.BadgeCategory.BRONZE
        self.points = 0

    def extended_description(self):
        return ("Breng je eerste positieve stem uit voor een nuttige vraag, antwoord "
                "of opmerking onder een video")

    def is_manually_awarded(self):
        return True


@badges.active_badge
class FirstDownVoteBadge(badges.Badge):

    def __init__(self):
        badges.Badge.__init__(self)
        self.description = "Duimen omlaag"
        self.badge_category = badges.BadgeCategory.BRONZE
        self.points = 0

    def extended_description(self):
        return ("Breng je eerste negatieve stem uit voor nutteloze vraag, "
                "antwoord, of opmerking onder een video")

    def is_manually_awarded(self):
        return True


@badges.active_badge
class ModeratorBadge(badges.Badge):

    def __init__(self):
        badges.Badge.__init__(self)
        self.description = "Beheerder"
        self.badge_category = badges.BadgeCategory.SILVER
        self.points = 0

        # Hidden badge
        self.is_hidden_if_unknown = True

    def extended_description(self):
        return ("Word beheerder van vragen, antwoorden en opmerkingen "
                "onder video&#39;s")

    def is_manually_awarded(self):
        return True


class FeedbackTimestampReferenceBadge(badges.Badge):
    """Badge for referencing a timestamp on a feedback entity (override
    required_feedback_type when subclassing)."""

    def __init__(self):
        badges.Badge.__init__(self)
        self.badge_category = badges.BadgeCategory.BRONZE
        self.badge_triggers.add(BadgeTriggerType.POST)
        self.points = 0

    def is_satisfied_by(self, *args, **kwargs):
        feedback = kwargs.get("feedback", None)
        if feedback is None:
            return False

        if not feedback.is_type(self.required_feedback_type()):
            return False

        r_timestamp = r'\b(\d+):([0-5]\d)\b'
        return bool(re.search(r_timestamp, feedback.content))


@badges.active_badge
class AnswerTimestampReferenceBadge(FeedbackTimestampReferenceBadge):
    """Badge for referencing a timestamp on an answer."""

    def __init__(self):
        FeedbackTimestampReferenceBadge.__init__(self)
        self.description = "Onderzoeker"

    def extended_description(self):
        return "Verwijs naar de datum wanneer je een vraag beantwoord bij een video"

    def required_feedback_type(self):
        return discussion.discussion_models.FeedbackType.Answer


@badges.active_badge
class QuestionTimestampReferenceBadge(FeedbackTimestampReferenceBadge):
    """Badge for referencing a timestamp on a question."""

    def __init__(self):
        FeedbackTimestampReferenceBadge.__init__(self)
        self.description = "Bibliograaf"

    def extended_description(self):
        return "Verwijs naar de datum wanneer je een vraag stelt bij een video"

    def required_feedback_type(self):
        return discussion.discussion_models.FeedbackType.Question
