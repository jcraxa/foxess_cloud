"""UI configuration for the original macxq FoxESS sensor engine."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "foxess"
API = "apiKey"
SN = "deviceSN"
FLAGS = ("extendPV", "xtZone", "Restrict", "Use_V1_Api", "Evo")

class FoxESSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            user_input["deviceID"] = user_input[SN]
            await self.async_set_unique_id(user_input[SN])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"FoxESS {user_input[SN]}", data=user_input
            )
        fields = {
            vol.Required(API): str,
            vol.Required(SN): str,
            vol.Optional("name", default="FoxESS"): str,
        }
        fields.update({vol.Optional(flag, default=False): bool for flag in FLAGS})
        return self.async_show_form(step_id="user", data_schema=vol.Schema(fields))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return FoxESSOptionsFlow(config_entry)

class FoxESSOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        fields = {
            vol.Optional(flag, default=self._entry.options.get(
                flag, self._entry.data.get(flag, False)
            )): bool for flag in FLAGS
        }
        return self.async_show_form(step_id="init", data_schema=vol.Schema(fields))
