from django.contrib import admin
from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'condition', 'created_at')
    list_filter = ('category', 'condition', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('ad_sender__title', 'ad_receiver__title', 'comment')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('ad_sender', 'ad_receiver')
