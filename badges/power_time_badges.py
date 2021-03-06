import datetime

import badges
import templatefilters


# All badges awarded for watching a specific amount of playlist time *and*
# completing a certain number of exercise problems within a set amount of time
# inherit from PowerTimeBadge
class PowerTimeBadge(badges.Badge):

    def is_satisfied_by(self, *args, **kwargs):
        action_cache = kwargs.get("action_cache", None)

        if action_cache is None:
            return False

        c_problem_logs = len(action_cache.problem_logs)
        c_video_logs = len(action_cache.video_logs)

        if c_video_logs < 1 or c_problem_logs < 1:
            return False

        latest_video_log = action_cache.get_video_log(c_video_logs - 1)
        date_video_end = latest_video_log.time_watched

        latest_problem_log = action_cache.get_problem_log(c_problem_logs - 1)
        date_problem_end = latest_problem_log.time_done

        date_end = max(date_video_end, date_problem_end)
        date_start = (date_end -
                      datetime.timedelta(seconds=self.seconds_allotted))

        seconds_watched = 0
        for i in range(c_video_logs):
            video_log = action_cache.get_video_log(c_video_logs - i - 1)
            if video_log.time_watched < date_start:
                break
            seconds_watched += video_log.seconds_watched

        if seconds_watched < self.video_seconds_required:
            return False

        problems_correct = 0
        for i in range(c_problem_logs):
            problem_log = action_cache.get_problem_log(c_problem_logs - i - 1)
            if problem_log.time_done < date_start:
                break
            if problem_log.correct:
                problems_correct += 1

        if problems_correct < self.problems_required:
            return False

        return True

    def extended_description(self):
        return "Beantwoord %s problemen correct en bekijk %s van de video van de %s" % (
            self.problems_required,
            templatefilters.seconds_to_time_string(
                self.video_seconds_required),
            templatefilters.seconds_to_time_string(self.seconds_allotted))


@badges.active_badge
class PowerFifteenMinutesBadge(PowerTimeBadge):

    def __init__(self):
        PowerTimeBadge.__init__(self)
        self.problems_required = 10
        self.video_seconds_required = 60 * 10
        self.seconds_allotted = 60 * 15
        self.description = "15 Minuten"
        self.badge_category = badges.BadgeCategory.BRONZE
        self.points = 0


@badges.active_badge
class PowerHourBadge(PowerTimeBadge):

    def __init__(self):
        PowerTimeBadge.__init__(self)
        self.problems_required = 90
        self.video_seconds_required = 15 * 60
        self.seconds_allotted = 3600
        self.description = "Power Uur"
        self.badge_category = badges.BadgeCategory.SILVER
        self.points = 0


@badges.active_badge
class DoublePowerHourBadge(PowerTimeBadge):

    def __init__(self):
        PowerTimeBadge.__init__(self)
        self.problems_required = 90 * 2
        self.video_seconds_required = 30 * 60
        self.seconds_allotted = 3600 * 2
        self.description = "Dubbel Power Uur"
        self.badge_category = badges.BadgeCategory.GOLD
        self.points = 0
