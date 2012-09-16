# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

class GroupDefaultOptionThroughInlineFormSet(BaseInlineFormSet):
    def clean(self):
        errors = []
        if self.forms:
            # count forms marked for deletion
            delete_forms = [form for form in self.initial_forms if self._should_delete_form(form)]
            deleted_forms_count = len(delete_forms)
            
            # count empty forms
            empty_forms = [form for form in self.extra_forms if not form.has_changed()]
            empty_forms_count = len(empty_forms)
            
            # calculate the resultant count after forms are saved
            resultant_forms_count = self.total_form_count() - deleted_forms_count - empty_forms_count
            
            if resultant_forms_count:
                # find a reference to the group
                group = None
                for form in self.forms:
                    if 'group' in form.cleaned_data:
                        group = form.cleaned_data['group']
                        break
                assert group is not None, "Forms did not reference 'group'"
                
                # count choices
                choose_count = group.get_choose_count()
                
                # compare the resultant count to the group's choice count
                if choose_count < resultant_forms_count:
                    errors.append(u"Option Group '%(group)s' only has %(choices)s choice%(pc)s.  You specified %(defaults)s default%(pd)s which is %(difference)s too many." % {
                            "group": group,
                            "choices": choose_count,
                            "defaults": resultant_forms_count,
                            "difference": (resultant_forms_count - choose_count),
                            "pc": "" if choose_count == 1 else "s",
                            "pd": "" if resultant_forms_count == 1 else "s"
                        }
                    )
        if errors:
            raise ValidationError(errors)