This program is a demonstration of 3 3D vector/point transformation methods I have learned recently. These are:
1. The perspective projection equation:
  The equation is: x' = x/z, y' = y/z
  An amazingly simple equation used to 'project' 3D coordinates into 2D space, which can then easily be converted into screen coordiantes.
  I learned this form Tsoding's video, it's a great watch: https://www.youtube.com/watch?v=qjWkNZ0SXfo
2. Vector rotations:
  I was messing around with vectors, and eventually derrived this equation by accident, when I realised it's just a trig identity.
  For rotations on the y axis it takes the format x' = x * cos(θ) - y * sin(θ), y' = x * sin(θ) + y * cos(θ)
3. Winding orientation:
  This equation is just a cross product between 2 vectors that returns a number more or less than zero depengin on if the second vector is to the left or right of the first
  winding = (p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x)
  this is used to determine the orientation of a face when applying textures to a triangle in 3D
