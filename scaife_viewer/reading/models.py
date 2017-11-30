from django.db import connection, models
from django.utils import timezone

from django.contrib.auth.models import User

from .. import cts


class ReadingLog(models.Model):
    user = models.ForeignKey(User)
    urn = models.CharField(max_length=250)
    timestamp = models.DateTimeField(default=timezone.now)

    @property
    def metadata(self):
        return metadata(self.urn)


def metadata(urn):
    try:
        passage = cts.passage(urn)
        parents = list(passage.text.ancestors())
        return {
            "textgroup_label": str(parents[1].label),
            "work_label": str(parents[0].label),
            "version_label": str(passage.text.label),
            "reference": str(passage.reference).replace("-", "–"),
            "lang": passage.text.lang,
        }
    except ValueError:
        return {}


def recent(user, limit=5):
    with connection.cursor() as cursor:
        sql = "SELECT urn, MAX(timestamp) AS timestamp FROM reading_readinglog WHERE user_id = %s GROUP BY urn ORDER BY timestamp DESC LIMIT %s"
        cursor.execute(sql, [user.pk, limit])

        return [
            {
                "metadata": metadata(row[0]),
                "urn": row[0],
                "timestamp": row[1],
            }
            for row in cursor.fetchall()
        ]


class ReadingList(models.Model):
    # @@@ we could use pinax teams and support membership, invitations,
    # @@@ permissions, etc
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)  # @@@ should this be unique?


class ReadingListEntry(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE, related_name="entries")
    urn = models.CharField(max_length=250)

    class Meta:
        order_with_respect_to = "reading_list"
