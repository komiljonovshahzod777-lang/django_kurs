from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "short_content", "created_at")
    list_filter = ("status", "created_at", "author")
    search_fields = ("title", "content", "author")
    list_editable = ("status",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 10
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("title", "author", "content"),
        }),
        ("Holat va sana", {
            "fields": ("status", "created_at", "updated_at"),
        }),
    )

    actions = ["make_published", "make_draft"]

    @admin.display(description="Qisqa matn")
    def short_content(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content

    @admin.action(description="Tanlanganlarni chop etish")
    def make_published(self, request, queryset):
        updated = queryset.update(status="published")
        self.message_user(request, f"{updated} ta maqola chop etildi.")

    @admin.action(description="Tanlanganlarni qoralamaga o'tkazish")
    def make_draft(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} ta maqola qoralamaga o'tkazildi.")


admin.site.site_header = "Mening Blog Admin Panelim"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Blogni boshqarish"
