help_add = '$add or $a: adds a character to your roster\n'\
           '     Syntax: $add <character name>, <class name>, <class engraving>, <item level>\n'\
           '     Example: $add Yuds, Sorceress, Reflux, 1510\n'\
           '     Notes: -user entry is not case sensitive\n'\
           '            -class names should NOT have spaces\n'\
           '            -use spaces where necessary when inputting class engraving (please follow\n             official in-game engraving naming schemes)\n'\
           '                 -e.g. 1: "Taijutsu" will not be accepted. Must input "Ultimate Skill:\n                           Taijutsu"\n'\
           '                 -e.g. 2: "Demonicimpulse" will not be accepted. Must input "Demonic\n                           Impulse"'

help_roster = "$roster or $r: view your own or someone else's roster\n"\
              "     Syntax: $roster <OPTIONAL @discord_name>\n"\
              "     Example 1: $roster\n"\
              "          This will display your own roster\n"\
              "     Example 2: $roster @Mokoko#6467\n "\
              "          This will display the roster whose discord tag is Mokoko#6467\n"

help_rankings = '$rankings: view the characters with the top 10 highest ilvls in this discord server\n'\
               "     Syntax: $rankings\n"\

help_statistics = "$statistics: view class distribution, ilvl distribution and average ilvl for your\n             discord server\n"\
                  "     Syntax: $statistics\n"

help_overview = "$overview: Displays everyone's roster in the specified discord server\n"\
                "     Syntax: $overview\n"

help_update = "$update or $u: Updates an attribute for one of your character in your roster\n"\
              "     Syntax: $update <character name>, <OPTIONS: name OR class OR ilvl OR engraving>,\n             <updated info>\n"\
              '     Example 1: To update character name from "Yuds" to "Mokoko" $update Yuds, name,\n             Mokoko\n'\
              '     Example 2: To update class to "Shadowhunter" $update Yuds, class, Shadowhunter\n'\
              '     Example 3: To update ilvl to 1600 $update Yuds, ilvl, 1600\n'\
              '     Example 4: To update engraving to "Igniter" $update Yuds, engraving, Igniter'

help_delete = "$delete or $d: deletes a character from your roster\n"\
              "     Syntax: $delete <character name>\n"\
              '     Example: To delete a character named "Yuds" from your roster $delete Yuds'

help = f'{help_add}\n\n'\
       f'{help_roster}\n\n'\
       f'{help_rankings}\n\n'\
       f'{help_statistics}\n\n'\
       f'{help_overview}\n\n'\
       f'{help_update}\n\n'\
       f'{help_delete}'

