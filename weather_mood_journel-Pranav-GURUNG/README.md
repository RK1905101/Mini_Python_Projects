This PR introduces a Flask backend for the Weather Mood Journal, allowing users to log moods along with weather context and manage their entries.

Features Implemented:

Log Mood (POST /log)

Create a new mood entry with date and weather.

Optional mood; if not provided, a random mood is suggested based on the weather.

Retrieve Entries (GET /entries)

Returns all logged entries in JSON format.

Get Suggested Moods (GET /moods?weather=)

Returns a list of suggested moods corresponding to a specific weather type.

Update Entry (PUT /update/)

Update an existing entry’s date, weather, or mood using its timestamp.

Delete Entry (DELETE /delete/)

Delete an entry by timestamp.
CSV Storage & Privacy

Entries are stored in mood_journal.csv.

CSV is not committed to the repo to protect user data.

.gitignore added to prevent committing sensitive logs.

CSV is initialized with headers if it doesn’t exist.

CSV Storage

Entries are stored in mood_journal.csv.

CSV is initialized with headers if it doesn’t exist.

Mood Map Dictionary (mood_map.py)

Stores moods associated with each weather type for automatic suggestions.