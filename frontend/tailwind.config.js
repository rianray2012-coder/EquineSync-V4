/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Cormorant Garamond"', 'serif'],
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      colors: {
        brand: {
          graphite: '#232734',
          slate: '#2E3550',
          frost: '#F7F8FA',
          mist: '#E3E6EB',
          lilac: '#B8AECF',
          lavender: '#D8D2E3',
          ice: '#DCEAF4',
          silverBlue: '#BCC9D6',
          text: '#1E2128',
          muted: '#667085',
          disabled: '#98A2B3',
          success: '#7FA98B',
          warning: '#D7B67A',
          critical: '#B46A6A',
        },
        equine: {
          /* Approved EquineSync brand aliases for product UI. */
          black:       '#F7F8FA',
          soft:        '#E3E6EB',
          card:        '#FFFFFF',
          elevated:    '#FFFFFF',
          tertiary:    '#ECEFF4',
          hairline:    '#E3E6EB',
          graphite:    '#BCC9D6',
          cloud:       '#E3E6EB',

          /* ============ TEXT ============ */
          ink:         '#1E2128',
          inkMuted:    '#667085',
          inkSoft:     '#98A2B3',

          /* ============ Legacy text aliases ============ */
          ivory:       '#1E2128',
          cream:       '#2E3550',
          silver:      '#667085',
          platinum:    '#98A2B3',

          /* ============ BRAND ACCENTS ============ */
          navy:        '#2E3550',
          navyDeep:    '#232734',
          navyLift:    '#37405E',
          lilac:       '#B8AECF',
          lilacDeep:   '#9F93BD',
          lavender:    '#D8D2E3',
          ice:         '#DCEAF4',
          silverBlue:  '#BCC9D6',
          steel:       '#DCEAF4',

          /* ============ STATUS (muted, refined) ============ */
          sage:        '#7FA98B',
          amber:       '#D7B67A',
          clay:        '#B46A6A',
          rose:        '#B46A6A',
          slate:       '#667085',
        },
        // ------------------------------------------------------------------
        // EquineSync Admin Portal palette (Brand Guide 22 — Admin-1).
        // Used EXCLUSIVELY for /admin/* surfaces. Do not bleed into the
        // marketing or product pages — they already have their lavender
        // palette above. These four tokens are an exact, locked match of
        // the master spec for the platform control center.
        // ------------------------------------------------------------------
        equinesync: {
          graphite: '#232734', // Midnight Graphite — primary surface for nav rail
          slate:    '#2E3550', // Slate Navy — accents, hovers, brand pills
          frost:    '#F7F8FA', // Frost White — main content bg, ink-on-graphite text
          lilac:    '#B8AECF', // Smoky Lilac — quiet accents, role pills, dividers
        },
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: { DEFAULT: 'hsl(var(--card))', foreground: 'hsl(var(--card-foreground))' },
        popover: { DEFAULT: 'hsl(var(--popover))', foreground: 'hsl(var(--popover-foreground))' },
        primary: { DEFAULT: 'hsl(var(--primary))', foreground: 'hsl(var(--primary-foreground))' },
        secondary: { DEFAULT: 'hsl(var(--secondary))', foreground: 'hsl(var(--secondary-foreground))' },
        muted: { DEFAULT: 'hsl(var(--muted))', foreground: 'hsl(var(--muted-foreground))' },
        accent: { DEFAULT: 'hsl(var(--accent))', foreground: 'hsl(var(--accent-foreground))' },
        destructive: { DEFAULT: 'hsl(var(--destructive))', foreground: 'hsl(var(--destructive-foreground))' },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      keyframes: {
        'accordion-down': { from: { height: '0' }, to: { height: 'var(--radix-accordion-content-height)' } },
        'accordion-up': { from: { height: 'var(--radix-accordion-content-height)' }, to: { height: '0' } },
        'fade-in': { from: { opacity: '0', transform: 'translateY(8px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.5s ease-out both',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
