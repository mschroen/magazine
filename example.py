# %%
from neatlogger import log

log.new("Welcome to the Magazine example!")

# Load this package
from magazine import Magazine, Publish

# %%
log.progress("Starting to do stuff and report on the way...")

# Magazine must be turned on or it wont record
Magazine.turn_on()

# Clean the content, only needed for repeated cell execution
Magazine.clean()

# Take some first notes
Magazine.report("Important topic", "The script has only {} characters.", 42)

# To showcase that reports can be made even in submodules
import example_submodule

example_submodule.myfunction()

# Add more notes
Magazine.report("Important topic", "And only {} spaces.", 7)

# Provide a citation, will be converted to full text later
Magazine.cite("10.1002/andp.19163540702")

# On a different topic, take notes as well
Magazine.report("Correction", "Everything on page 1 is wrong.")

# Make a plot with the matplotlib wrapper from figurex.
# The "agg" backend is important for later PDF export.
from figurex import Figure

with Figure(backend="agg", show=False) as ax:
    ax.plot([1, 2], [3, 4])

# Store the plot into the Magazine as well
Magazine.report("Important topic", Figure.as_object())


# Instead of inline commands, you can also use a decorator:
@Magazine.reporting("Physics")
def Method_A(a, b, c=3):
    """
    A complex method to calculate the sum of numbers.

    Report
    ------
    The method "{function}" used input parameters a={a}, b={b}, and c={c}.
    Calculations have been performed following Einstein et al. (1935).
    The result was: {return}. During the process, the magic number {magic} appeared.

    References
    ----------
    Einstein, A., Podolsky, B., & Rosen, N. (1935). Can Quantum-Mechanical Description of Physical Reality Be Considered Complete? Physical Review, 47(10), 777–780. https://doi.org/10.1103/physrev.47.777

    """
    result = a + b + c

    magic = 42

    return result


# When the function is called, it is automatically reported.
Method_A(2, 3, c=4)


# %%
log.write("Publishing...")

# Collect all notes and write the report into the Magazine.
with Publish("output/Magazine.pdf", "My Magazine", info="Version 1.0") as M:
    for topic in Magazine.topics:
        M.add_topic(topic)
        M.add_figure(topic)

    # Reference page
    M.add_references()
