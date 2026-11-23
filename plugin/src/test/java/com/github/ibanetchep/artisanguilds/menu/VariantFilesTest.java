package com.github.ibanetchep.artisanguilds.menu;

import net.artisanmc.modules.api.template.TemplateDeclaration;
import org.junit.jupiter.api.Test;
import org.yaml.snakeyaml.Yaml;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/** The Bedrock and textured versions of the menus the module ships. */
class VariantFilesTest {

    private static final Pattern OTHER_CLICK =
            Pattern.compile("^\\s*(right|shift_left|shift_right|middle|drop)\\s*:", Pattern.MULTILINE);
    /** An image a menu names: a button's {@code asset:} or a title layer's {@code asset_id:}. */
    private static final Pattern ASSET = Pattern.compile("\\basset(_id)?:\\s*\"?([a-z0-9_]+)");

    private static TemplateDeclaration files() {
        return TemplateDeclaration.fromResources(VariantFilesTest.class.getClassLoader(), GuildsModule.SYSTEM_ROOT,
                GuildsModule.SYSTEM, GuildsModule.SYSTEM_VERSION, GuildsModule.SYSTEM_FILES).build();
    }

    /**
     * A variant's menu takes the inputs of the module's menu (Artisan leaves it out otherwise, and
     * its players silently get the module's), and the Bedrock versions only use the left click,
     * the only one Bedrock sends.
     */
    @Test
    void variantsKeepTheInputsAndBedrockOnlyTaps() {
        TemplateDeclaration files = files();
        int bedrock = 0, textured = 0;
        for (String path : files.getPaths()) {
            if (!path.startsWith("variants/")) continue;
            String[] parts = path.split("/", 3);
            String text = new String(files.getFile(path), StandardCharsets.UTF_8);
            Map<String, Object> variant = new Yaml().load(text);
            assertNotNull(files.getFile(parts[2]), parts[2]);
            Map<String, Object> module = new Yaml().load(new String(files.getFile(parts[2]), StandardCharsets.UTF_8));
            assertEquals(module.get("inputs"), variant.get("inputs"), path);
            if (parts[1].equals("bedrock")) {
                bedrock++;
                assertFalse(OTHER_CLICK.matcher(text).find(), path);
            } else {
                textured++;
            }
        }
        assertEquals(4, bedrock);
        // Every menu of the module.
        assertEquals(files.getPaths().stream().filter(p -> p.startsWith("menus/")).count(), textured);
    }

    /**
     * The textured menus name only shipped images, every shipped image is named, and each image's
     * descriptor gives its real size (the pack places it by that size).
     */
    @Test
    void texturedImagesAreShippedUsedAndSized() throws IOException {
        TemplateDeclaration files = files();
        Set<String> named = new TreeSet<>();
        for (String path : files.getPaths()) {
            if (!path.startsWith("variants/textured/")) continue;
            Matcher m = ASSET.matcher(new String(files.getFile(path), StandardCharsets.UTF_8));
            while (m.find()) named.add((m.group(1) != null ? "glyphs/" : "textures/") + m.group(2));
        }
        Set<String> shipped = new TreeSet<>();
        for (String path : files.getPaths()) {
            if (!path.startsWith("assets/") || !path.endsWith(".png")) continue;
            String name = path.substring("assets/".length(), path.length() - ".png".length());
            shipped.add(name);
            byte[] descriptor = files.getFile("assets/" + name + ".yml");
            assertNotNull(descriptor, name + ".yml");
            Map<String, Object> size = new Yaml().load(new String(descriptor, StandardCharsets.UTF_8));
            BufferedImage image = ImageIO.read(new ByteArrayInputStream(files.getFile(path)));
            assertEquals(image.getWidth(), size.get("width"), name);
            assertEquals(image.getHeight(), size.get("height"), name);
        }
        assertEquals(shipped, named);
    }
}
