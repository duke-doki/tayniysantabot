from django.contrib import admin

from santa.models import Person, Party, Message, Answer, AllowedIdentifier, \
    Winner


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_filter = ('is_owner', 'is_organizer', 'is_player')


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_filter = ('cost_limit', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', )


@admin.register(AllowedIdentifier)
class AllowedIdentifierAdmin(admin.ModelAdmin):
    list_display = ('username', )


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_filter = ('santa', 'party', )
