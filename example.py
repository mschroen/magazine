# %%
from neatlogger import log

log.new("Welcome to the Magazine example!")

# Load this package
from magazine import Story, Publish

# If you want to make a plot, load this matplotlib wrapper
from figurex import Figure

# To showcase that stories can be told even in submodules
import example_submodule

# %%
log.progress("Writing stories...")
# Clean stories, only needed for repeated cell execution
Story.clean()

# Take some first notes
Story.report("Important topic", "The script has only {} characters.", 42)
# Let the submodule take some notes
example_submodule.myfunction()
# Add more notes
Story.cite("10.1002/andp.19163540702")

Story.report("Important topic", "And only {} spaces.", 7)
# On a different topic, take notes as well
Story.report("Correction", "Everything on page 1 is wrong.")

# Make a plot, the "agg" backend is important for later PDF export
with Figure(backend="agg", show=False) as ax:
    ax.plot([1, 2], [3, 4])
# Store the plot into your notebook as well
Story.report("Important topic", Figure.as_object(ax))
Story.cite("10.1103/PhysRev.47.777")

# %%
log.write("Publishing...")
# Collect all notes and write the stories into the magazine PDF.
with Publish("output/Magazine.pdf", "My Magazine", info="Version 0.1") as M:
    for story in Story.stories:
        M.add_story(story)
        M.add_figure(story)

    # Reference page
    M.add_references()
