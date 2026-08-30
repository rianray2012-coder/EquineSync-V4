import React from "react";
import { Link } from "react-router-dom";
import horseFrost from "../assets/brand/icon_horse_frost.png";
import horseDark from "../assets/brand/icon_horse_dark.png";
import horseFrostSquare from "../assets/brand/icon_horse_frost_square.png";
import horseDarkSquare from "../assets/brand/icon_horse_dark_square.png";

/**
 * Official EquineSync brand mark.
 * Running-horse icon (frost-on-transparent for dark surfaces, graphite+lilac for light)
 * paired with a CSS-composed "EquineSync" wordmark — "Sync" in Smoky Lilac.
 *
 * API preserved from the previous placeholder: `size`, `withText`, `onNavy`.
 * Added (additive, optional): `variant` ('horizontal' | 'icon'), `tone` ('dark' | 'light').
 */
export const Logo = ({
  size = 36,
  withText = true,
  onNavy = false,
  variant = "horizontal",
  tone,
  linkTo = "/",
}) => {
  const dark = tone ? tone === "dark" : onNavy;
  const wordmarkSize = Math.max(22, Math.round(size * 0.61));
  const taglineSize = Math.max(8.5, Number((size * 0.235).toFixed(1)));
  const markGap = Math.max(12, Math.round(size * 0.33));

  // Guide 22 logo color application (logo-color correctness only; not an app-palette change)
  const equineColor = dark ? "#F7F8FA" : "#1E2128";
  const syncColor = "#B8AECF";
  const taglineColor = dark ? "#BCC9D6" : "#667085";

  const iconSrc = variant === "icon"
    ? (dark ? horseFrostSquare : horseDarkSquare)
    : (dark ? horseFrost : horseDark);

  const iconEl = (
    <img
      src={iconSrc}
      alt="EquineSync"
      style={{ height: size, width: "auto" }}
      className="object-contain shrink-0 select-none transition-opacity duration-300 group-hover/logo:opacity-80"
      draggable={false}
    />
  );

  const Wrapper = linkTo ? Link : "span";
  const wrapperProps = linkTo
    ? { to: linkTo, "aria-label": "EquineSync home" }
    : {};

  if (variant === "icon" || !withText) {
    return (
      <Wrapper
        {...wrapperProps}
        className="group/logo inline-flex items-center focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-lilac/70 focus-visible:ring-offset-2 focus-visible:ring-offset-transparent"
        data-testid={linkTo ? "logo-home-link" : "logo"}
      >
        {iconEl}
      </Wrapper>
    );
  }

  return (
    <Wrapper
      {...wrapperProps}
      className="group/logo flex items-center focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-lilac/70 focus-visible:ring-offset-2 focus-visible:ring-offset-transparent"
      style={{ gap: markGap }}
      data-testid={linkTo ? "logo-home-link" : "logo"}
    >
      {iconEl}
      <div className="leading-none">
        <div className="font-display tracking-wide" style={{ fontSize: wordmarkSize }}>
          <span style={{ color: equineColor }}>Equine</span>
          <span style={{ color: syncColor }}>Sync</span>
        </div>
        <div
          className="tracking-[0.22em] uppercase mt-1.5 font-medium"
          style={{ color: taglineColor, fontSize: taglineSize }}
        >
          Every Horse. Every Task. In Sync.
        </div>
      </div>
    </Wrapper>
  );
};
