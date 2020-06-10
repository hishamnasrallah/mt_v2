from import_export import resources
from .models import TranslationHistory


class TranslationHistoryResource(resources.ModelResource):
    class Meta:
        model = TranslationHistory
        fields = ('to_translate', 'translated', 'created_by__username', 'client__name', 'created_date',)
        # exclude = ('updated_by', 'updated_date',)

    def export(self, queryset=None, *args, **kwargs):
        queryset = TranslationHistory.objects.filter()
        return super(TranslationHistoryResource, self).export(queryset, *args, **kwargs)