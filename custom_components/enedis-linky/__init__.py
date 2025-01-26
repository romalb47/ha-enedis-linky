DOMAIN = "enedis_linky"


def setup(hass, config):
    hass.states.set("enesis_linky.world", "Paulus")

        # Return boolean to indicate that initialization was successful.
            return True