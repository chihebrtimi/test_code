from django.core.management.base import BaseCommand
from monitoring.models import SensorData
from django.utils import timezone
import pandas as pd
import os

class Command(BaseCommand):
    help = "Export and delete sensor data older than 30 days"

    def handle(self, *args, **kwargs):
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        old_data = SensorData.objects.filter(timestamp__lt=thirty_days_ago)

        if not old_data.exists():
            self.stdout.write("No old data to archive.")
            return

        df = pd.DataFrame.from_records(old_data.values())
        os.makedirs("exports", exist_ok=True)
        filename = f"exports/backup_{timezone.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        df.to_excel(filename, index=False)
        old_data.delete()

        self.stdout.write(f"✅ Exported and deleted {len(df)} records.")
