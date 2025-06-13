# AthleteAce JSON Templates

This directory contains JSON templates for all supported data formats in AthleteAce. Use these templates when contributing new sports data to the project.

## Template Files

### Core Sports Data
- **`sports.json`** - Sport definitions (Baseball, Basketball, etc.)
- **`leagues.json`** - League information within a sport/country
- **`conferences.json`** - Conference and division structure
- **`teams.json`** - Team information including colors, logos, stadiums
- **`players.json`** - Individual player data and statistics
- **`memberships.json`** - Historical team-division relationships
- **`seasons.json`** - Season dates, format, and metadata
- **`positions.json`** - Sport-specific player positions

### Location Data
- **`countries.json`** - Country information with ISO codes
- **`states.json`** - States/provinces within countries  
- **`cities.json`** - Cities within states
- **`stadiums.json`** - Stadium/venue information

### Contest & Achievement Data
- **`contests.json`** - Competitions, tournaments, regular seasons
- **`quests.json`** - Achievements and quest definitions
- **`spectrums.json`** - Rating scales and measurement systems

### Historical Data
- **`expansions.json`** - Team expansion campaigns
- **`transitions.json`** - Team relocations, rebrands, name changes
- **`federations.json`** - International governing bodies

## Usage Guidelines

1. **Follow the schema** - Each template shows required and optional fields
2. **Use consistent naming** - Follow existing naming conventions in the data
3. **Include metadata** - Add descriptions, URLs, and logos where available
4. **Validate relationships** - Ensure team names match across files
5. **Use ISO standards** - Country codes, date formats, etc.

## File Locations

Place your JSON files in the appropriate directory structure:

```
db/seeds/athlete_ace_data/
├── sports/
│   └── [sport_name]/
│       └── [country]/
│           ├── leagues.json
│           └── [league_name]/
│               ├── conferences.json
│               ├── teams.json
│               ├── memberships.json
│               ├── seasons.json
│               ├── contests/
│               │   └── *.json
│               └── players/
│                   └── [team_name].json
├── locations/
│   ├── countries/
│   ├── states/
│   ├── cities/
│   └── stadiums/
├── quests/
├── ratings/
└── federations/
```

## Contributing

When adding new data:

1. Start with location data (country → state → city → stadium)
2. Add sport and league structure
3. Create teams and assign to divisions
4. Add players and historical data
5. Create contests and achievements

For questions or help, please refer to the main AthleteAce documentation.