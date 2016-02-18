# Change Log

## 1.2.0

* Rename to pinax.announcements
* Drop support for django < 1.5
* Rewrite docs for readthedocs with markdown (template based on pinax-blog)
* Update test config (travis, tox, coveragerc, ...)
* Update .gitignore
* Generate django migrations
* Move templates to pinax/announcements/

## 1.0.1

* fixed included templates to be compatible with Django 1.5


## 1.0

* removed atom feed
* renamed dismiss url
* switched to timezone.now
* marked some choice field strings for translation
* swapped view mixin override in favor of auth backend and permission checking

## 0.2

* added ability to publish for periods of time
* added model to store permanent clearings (see migration below)
* added ability to control how announcements are cleared (no
  clearing, session based, or permanent) (see migration below)
* changed view `announcement_hide` to `dismiss`
* changed url name of `announcement_hide` to `announcement_dismiss`
* changed template tag from fetch_announcements to announcements
* removed send now functionality
* removed notifications
* removed context processor
* removed list view
* removed AnnouncementsManager
* removed current_announcements_for_request


## Migrations

Migration scripts to move prior installations to latest version::

    ALTER TABLE "announcements_announcement" ADD COLUMN "dismissal_type" int DEFAULT 2 NOT NULL;
    ALTER TABLE "announcements_announcement" ADD COLUMN "publish_start" timestamp with time zone NOT NULL;
    ALTER TABLE "announcements_announcement" ADD COLUMN "publish_end" timestamp with time zone;
    ### New Model: announcements.Dismissal
    CREATE TABLE "announcements_dismissal" (
        "id" serial NOT NULL PRIMARY KEY,
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "announcement_id" integer NOT NULL REFERENCES "announcements_announcement" ("id") DEFERRABLE INITIALLY DEFERRED,
        "dismissed_at" timestamp with time zone NOT NULL
    )
    ;
    CREATE INDEX "announcements_dismissal_user_id" ON "announcements_dismissal" ("user_id");
    CREATE INDEX "announcements_dismissal_announcement_id" ON "announcements_dismissal" ("announcement_id");


## 0.1

* initial release
