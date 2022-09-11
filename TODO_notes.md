Buildings that take more than one cell need to be objects not tiles for proper y-sort - otherwise player clips via top cells - done

collsision object should fill in thier cells more fully to avoid creating "invisible wall" feeling - separate small collision boxes

Player collision box should be customizable individually. - lets use standard half height for all objects

Refactor animation system, because the one in tutorial is just awful. Use somekind of simple state machine. - Done

Find solution for getting close to borders -  I just have extra unreachable level area

Make movement with acceleration and breaking instead of current 01

Have camera on on "rubber"