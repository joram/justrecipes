#!/usr/bin/env python3
import json
import os


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(current_dir, f"../recipes/data/")
    dest_dir = os.path.join(current_dir, f"./public/recipes/")
    os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
    file_names = os.listdir(src_dir)

    # copy over
    manifest = {"recipes": []}
    for file_name in file_names:
        if not file_name.endswith(".json"):
            continue
        source = os.path.join(src_dir, file_name)
        destination = os.path.join(dest_dir, file_name)
        with open(source) as f:
            content = f.read()
            with (open(destination, "w")) as f:
                f.write(content)
            content = json.loads(content)
            image_url = content["image_urls"][0]
            title = content["name"]
            manifest["recipes"].append({"image": image_url, "title": title})


    # update the manifest
    with open(f"{dest_dir}/../../src/recipe_manifest.json", "w") as f:
        content = json.dumps(manifest, indent=2, sort_keys=True)
        f.write(content)

    print(f"updated {len(manifest['recipes'])} recipes, and manifest")