import texturaMar from '../assets/coronel-mar.svg?raw'
import texturaIndustria from '../assets/coronel-industria.svg?raw'

const texturas = {
  mar: texturaMar,
  industria: texturaIndustria,
}

type CoronelTextureProps = {
  variant: keyof typeof texturas
}

export default function CoronelTexture({ variant }: CoronelTextureProps) {
  return <div
    className={`local-texture local-texture-${variant}`}
    aria-hidden="true"
    dangerouslySetInnerHTML={{ __html: texturas[variant] }}
  />
}
