package com.github.ibanetchep.artisanguilds.chat;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.TextComponent;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.format.TextColor;
import net.kyori.adventure.text.minimessage.MiniMessage;
import org.bukkit.configuration.file.YamlConfiguration;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
 * The guild and alliance chat lines of the jar's lang files read as MSGuilds' did: the prefix, the
 * player's name and the message in gray, only the arrow in white, whatever colour the rank leaves open.
 */
class ChatFormatTest {

    @ParameterizedTest
    @CsvSource({"fr, guild_format", "fr, ally_format", "en, guild_format", "en, ally_format"})
    void theLineIsGrayAroundAWhiteArrow(String lang, String key) throws Exception {
        String format;
        try (var in = getClass().getResourceAsStream("/lang/" + lang + ".yml")) {
            assertNotNull(in, lang);
            format = YamlConfiguration.loadConfiguration(new InputStreamReader(in, StandardCharsets.UTF_8))
                    .getString("messages.chat." + key);
        }
        assertNotNull(format, lang + " " + key);

        String line = format.replace("%rank%", "<red>Chef")
                .replace("%player%", "Bob").replace("%message%", "salut");
        Map<String, TextColor> colours = new LinkedHashMap<>();
        collect(MiniMessage.miniMessage().deserialize(line), null, colours);

        assertEquals(NamedTextColor.GRAY, colours.get("Bob"), "player in " + lang + " " + key);
        assertEquals(NamedTextColor.WHITE, colours.get("➤"), "arrow in " + lang + " " + key);
        assertEquals(NamedTextColor.GRAY, colours.get("salut"), "message in " + lang + " " + key);
    }

    /** Each piece of text with the colour it is shown in: its own, else its parents'. */
    private static void collect(Component c, TextColor inherited, Map<String, TextColor> out) {
        TextColor colour = c.color() != null ? c.color() : inherited;
        if (c instanceof TextComponent t && !t.content().isBlank()) out.put(t.content().trim(), colour);
        for (Component child : c.children()) collect(child, colour, out);
    }
}
