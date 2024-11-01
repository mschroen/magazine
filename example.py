# %%
import sys
from loguru import logger as log
log.remove()
log.add(sys.stderr, colorize=True, format="<level>{level: <8}</> <level>{message}</>")

from magazine import Story, Publish

Story.report("Important topic","The script has only {} characters.", 42)
import example_submodule
example_submodule.myfunction()
Story.report("Important topic","And only {} spaces.", 7)
Story.report("Correction","Everything on page 1 is wrong.")

with Publish("output/Magazine.pdf", "My Magazine", info="Version 0.1") as M:
    
    for story in Story.stories:
        M.add_story(story)

