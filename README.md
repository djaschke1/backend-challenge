# The Q-CTRL Back-end Challenge

The goal of this challenge is to create a web-based API using [Django](https://www.djangoproject.com/). The API should be backed by a [MySQL](https://www.mysql.com/) database and conform to the [JSON API](http://jsonapi.org/) specification.

To get started please fork this repository and when you're finished create a pull request.

## Brief

The brief has been divided into three parts:

1.  [Manage pulses](#manage-pulses)
1.  [Upload pulses](#upload-pulses)
1.  [Download pulses](#download-pulses)

---

### Manage pulses

Implement endpoints that can:

- Create a new pulse
- List all pulses (five per page)
- Get a specific pulse
- Update a specific pulse
- Delete a specific pulse

---

### Upload pulses

Implement an endpoint that can accept a [CSV file](doc/files/pulses.csv) where each row represents a pulse.

---

### Download pulses

Implement an endpoint that returns all pulses in CSV format. The CSV should not include a header row.

---

## Additional Information

Below are the attributes of a pulse. All attributes are required.

| Name              | Type   | Description                                                                         |
|-------------------|--------|-------------------------------------------------------------------------------------|
| name              | string | The name of the pulse (e.g. "My Awesome Pulse")                                     |
| type              | string | The type of pulse. Valid pulse types are: primitive, corpse, gaussian, cinbb, cinsk |
| maximum_rabi_rate | float  | A floating-point number between 0 and 100                                           |
| polar_angle       | float  | A floating-point number between 0 and 1                                             |
