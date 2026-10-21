# frozen_string_literal: true

require "yaml"
require "json"
require "fileutils"

root = File.expand_path("..", __dir__)
output = File.join(root, "yaml/participation")
FileUtils.mkdir_p(output)
capture = JSON.parse(File.read(File.join(root, "sources/coverage_2025.json")))
sources = capture.fetch("teams").to_h { |team| [ [ team.fetch("league"), team.fetch("abbreviation") ], team ] }
organizations, rosters = [], []
Dir.glob(File.join(root, "yaml/coverage_2025/*.yaml")).sort.each do |path|
  manifest = YAML.safe_load_file(path)
  league = File.basename(path, ".yaml").upcase
  manifest.fetch("groups").each do |group|
    team_code = group.fetch("scope").fetch("team")
    campaign = group.fetch("records").find { |record| record.fetch("type") == "Campaign" }
    team = sources.fetch([ league, campaign.fetch("attributes").fetch("abbreviation") ])
    organization_code = team_code.sub("-TEAM-", "-ORG-")
    source = group.fetch("source")
    organizations << { "source" => source, "records" => [
      { "type" => "Organization", "code" => organization_code,
        "attributes" => { "name" => team.fetch("name"), "abbreviation" => team.fetch("abbreviation"),
          "description" => "Sporting club organization; this record does not identify a legal corporate owner." } },
      { "type" => "OrganizationAffiliation", "code" => "#{organization_code}-TEAM-#{team_code.split('-TEAM-').last}",
        "attributes" => { "details" => { "relationship" => "senior_team", "date_precision" => "unknown", "source" => source } },
        "references" => { "organization" => organization_code, "team" => team_code } }
    ] }

    next if league == "NHL"
    kind = { "NBA" => "published_season_roster", "NFL" => "published_season_player_inventory", "EPL" => "senior_registration" }.fetch(league)
    suffix = league == "EPL" ? "SENIOR_REGISTRATION_2025_09_12" : "CAPTURE_#{capture.fetch('captured_on').tr('-', '_')}"
    roster_code = "#{campaign.fetch('code')}-ROSTER-#{suffix}"
    attributes = { "kind" => kind, "coverage" => campaign.fetch("attributes").fetch("details").fetch("roster_coverage") == "complete_source_listing" ? "complete" : "partial",
      "details" => campaign.fetch("attributes").fetch("details") }
    attributes["effective_on"] = "2025-09-12" if league == "EPL"
    entries = group.fetch("records").select { |record| record.fetch("type") == "Activation" }.map do |activation|
      player = activation.fetch("references").fetch("player")
      { "type" => "RosterEntry", "code" => "#{roster_code}-PLAYER-#{activation.fetch('code').split('-PLAYER-').last}",
        "references" => { "roster" => roster_code, "player" => player } }
    end
    rosters << { "source" => source, "records" => [
      { "type" => "Roster", "code" => roster_code, "attributes" => attributes, "references" => { "campaign" => campaign.fetch("code") } },
      *entries
    ] }
  end
end
header = { "format" => "micharisma-seeds/v1", "namespace" => "MIC", "catalog" => "ALA" }
# Copy shared objects so Psych emits no anchors/aliases, which the safe reader rejects.
File.write(File.join(output, "organizations.yaml"), YAML.dump(JSON.parse(JSON.generate(header.merge("groups" => organizations)))))
File.write(File.join(output, "rosters_2025.yaml"), YAML.dump(JSON.parse(JSON.generate(header.merge("groups" => rosters)))))
puts JSON.generate(organizations: organizations.size, affiliations: organizations.size, rosters: rosters.size,
  roster_entries: rosters.sum { |group| group.fetch("records").size - 1 })
