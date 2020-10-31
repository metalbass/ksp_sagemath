from math import sqrt, sin

GRAVITATIONAL_CONSTANT = 6.6743E-11 # m^3 / (kg s^2)

class Body:
	def __init__(self, name, mass, radius):
		self.name = name
		self.mass = mass
		self.radius = radius

	def __repr__(self):
		return f'Body(\'{self.name}\', mass={self.mass}, radius={self.radius})'

class Orbit:
	def __init__(self, body, apoapsis, periapsis, inclination = 0):
		self.body = body
		self.semimajor_axis = body.radius + (apoapsis + periapsis) / 2

		self.focus = self.semimajor_axis - (periapsis + body.radius)

		self.semiminor_axis = sqrt(pow(self.semimajor_axis, 2) - pow(self.focus, 2))

		self.inclination = inclination

	def __repr__(self):
		return f'Orbit(\'{self.body.name}\', apoapsis={self.apoapsis()}, periapsis={self.periapsis()}, inclination={self.inclination})'

	def apoapsis(self):
		return self.semimajor_axis + self.focus - self.body.radius

	def periapsis(self):
		return self.semimajor_axis - (self.focus + self.body.radius)

	def velocity_at_apoapsis(self):
		return self.velocity_at(self.apoapsis())

	def velocity_at_periapsis(self):
		return self.velocity_at(self.periapsis())

	def velocity_at(self, height):
		r = height + self.body.radius

		mu =  GRAVITATIONAL_CONSTANT * self.body.mass
		return sqrt(mu*((2 / r) - (1 / self.semimajor_axis)))


class Maneuvers:
	def InclinationChange(start_orbit, height, desired_inclination):
		inclination_change = desired_inclination - start_orbit.inclination

		velocity_at_height = start_orbit.velocity_at(height)

		return 2 * velocity_at_height * sin(inclination_change / 2)

	def HommannTransfer(from_orbit, to_orbit):
		transfer_orbit = Orbit(from_orbit.body, apoapsis=to_orbit.apoapsis(), periapsis=from_orbit.apoapsis(), inclination=from_orbit.inclination)

		deltaV = 0
		deltaV += transfer_orbit.velocity_at_periapsis() - from_orbit.velocity_at_periapsis()
		deltaV += to_orbit.velocity_at_apoapsis() - transfer_orbit.velocity_at_apoapsis()

		return deltaV
