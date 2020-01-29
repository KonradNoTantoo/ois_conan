from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds()
    builder.remove_build_if(lambda build: build.settings["arch"] == "x86")
    builder.run()
