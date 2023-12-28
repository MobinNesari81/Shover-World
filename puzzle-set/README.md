# Puzzles #

Here are some puzzles designed to practice Shover.

Each puzzle is defined by an 32x32 array in json format.

The objects on the Shover board are defined by elements of the array, as follows;
- [0] free board tile (un-occupied).
- [1] box.
- [-1] hole (void space).
- [10] or any integer number divisible by 10, except 0, obstacle.

The last six elements of the last row of the array are extra info with the following meanings;
* 1000 + the number of boxes.
* 1000 + the number of obstacles.
* 1000 + the number holes.
* 1000 + puzzle uid.
* 1000 + puzzle id (could be considered as the difficulty level).
* 1000 + A minimum record of the total force required to push out all boxes into void.

## Note. ##
In the present version, all the puzzles maps are 9x13, hence, including the void margins, the elements outside of the upper-left 11x15 sub-array, in fact, are un-used.
