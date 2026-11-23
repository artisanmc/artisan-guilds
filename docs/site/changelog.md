---
title: Changelog
description: The versions of Artisan Guilds, newest first.
sidebar:
  order: 6
---

## 2.0.0 (unreleased)

- MSGuilds becomes Artisan Guilds, a module of Artisan: requires Artisan API 1.0.0, no longer Core.
- Guilds imported once from Core's database; MSGuilds' config and edited lang files copied.
- Menus and dialogs are Artisan menus (guild, members, ranks, rank permissions, confirmations).
- Textured menus: Java players who loaded the resource pack see every guild menu drawn with images, same clicks. The bank box shortens the balance (18.4K, 1.8M, up to T; `guilds:guild` field `balance_short`), the exact sum on hover.
- Alliances menu (`/g alliance`): allies, offers to accept, offers sent, ending an alliance; the guild menu also switches the chat mode.
- Language and levels in the module settings, edited in the editor; levels add a member cap and a chest size.
- Guild chest (`/g chest`), one server per network.
- MSGuildQuests becomes ArtisanGuildQuests, built in this repository.
