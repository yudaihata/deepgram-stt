# Integration brand images

The `custom_components/deepgram_stt/brand/` directory contains the official
Deepgram square lettermark, rendered as PNG at 256 and 512 pixels for Home
Assistant's local brand API (Home Assistant 2026.3+). The square mark also serves
as the logo through Home Assistant's built-in fallback. Both light and dark
variants are included.

Source: Deepgram's [`@deepgram/styles` package, v0.2.15](https://www.npmjs.com/package/@deepgram/styles/v/0.2.15),
`dist/logo/lettermark-square-light.svg` and `lettermark-square-dark.svg`.
See the [official logo reference](https://design.dx.deepgram.com/brand/foundations/logos).
The PNG files are direct CairoSVG renders of those SVG assets at the required
sizes. Deepgram's name and marks belong to Deepgram; their inclusion identifies
the service used by this community integration.
