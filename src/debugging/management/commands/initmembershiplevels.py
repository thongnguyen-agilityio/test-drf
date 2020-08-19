from django.core.management.base import BaseCommand

from app.constants import MembershipSettings
from customers.models import MembershipLevel


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Init membership levels like a linked list.
        """
        try:
            num_settings = len(MembershipSettings)
            for index, setting in enumerate(MembershipSettings):
                # Check and create current setting
                if setting and 'position' in setting.keys():
                    setting.pop('position')

                current_setting_obj = MembershipLevel.objects.filter(
                    name=setting.get('name')
                ).first()

                if not current_setting_obj:
                    current_setting_obj = MembershipLevel.objects.create(
                        **setting,
                    )

                # Check and create next setting
                if index + 1 >= num_settings:
                    return

                next_setting = MembershipSettings[index + 1] \
                    if index + 1 < num_settings else None

                if next_setting and 'position' in next_setting.keys():
                    next_setting.pop('position') if next_setting else None

                next_setting_obj = MembershipLevel.objects.filter(
                    name=next_setting.get('name')
                ).first()

                if not next_setting_obj:
                    next_setting_obj = MembershipLevel.objects.create(
                        previous=current_setting_obj,
                        **next_setting,
                    )
                else:
                    next_setting_obj.previous = current_setting_obj
                    next_setting_obj.save()

                current_setting_obj.next = next_setting_obj
                current_setting_obj.save()
        except Exception as e:
            raise e
