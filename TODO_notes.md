Buildings that take more than one cell need to be objects not tiles for proper y-sort - otherwise player clips via top cells
collsision object should fill in thier cells more fully to avoid creating "invisible wall" feeling
Player collision box should be customizable individually.

Refactor animation system, because the one in tutorial is just awful. Use somekind of simple state machine.

Find solution for getting close to borders - should camera stop or should I just have extra unreachable level area

Make movement with acceleration and breaking instead of current 01

Have camera on on "rubber"