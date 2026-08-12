"use client";

import {
  Monitor,
  Moon,
  Sun,
} from "lucide-react";

import {
  useEffect,
  useState,
} from "react";

type Theme = "system" | "light" | "dark";

const themes: {
  value: Theme;
  label: string;
  icon: typeof Monitor;
}[] = [
  {
    value: "system",
    label: "System",
    icon: Monitor,
  },
  {
    value: "light",
    label: "Light",
    icon: Sun,
  },
  {
    value: "dark",
    label: "Dark",
    icon: Moon,
  },
];

export default function ThemeSwitcher() {
  const [theme, setTheme] =
    useState<Theme>("dark");

  useEffect(() => {
    const storedTheme =
      localStorage.getItem(
        "rag-assistant-theme"
      ) as Theme | null;

    if (
      storedTheme === "system" ||
      storedTheme === "light" ||
      storedTheme === "dark"
    ) {
      setTheme(storedTheme);
      applyTheme(storedTheme);
    } else {
      applyTheme("dark");
    }
  }, []);

  function applyTheme(nextTheme: Theme) {
    const root =
      document.documentElement;

    root.classList.remove(
      "light",
      "dark"
    );

    if (nextTheme === "system") {
      const prefersDark =
        window.matchMedia(
          "(prefers-color-scheme: dark)"
        ).matches;

      root.classList.add(
        prefersDark ? "dark" : "light"
      );

      return;
    }

    root.classList.add(nextTheme);
  }

  function handleThemeChange(
    nextTheme: Theme
  ) {
    setTheme(nextTheme);

    localStorage.setItem(
      "rag-assistant-theme",
      nextTheme
    );

    applyTheme(nextTheme);
  }

  return (
    <div className="grid grid-cols-3 gap-2">
      {themes.map((item) => {
        const Icon = item.icon;

        const isActive =
          theme === item.value;

        return (
          <button
            key={item.value}
            type="button"
            onClick={() =>
              handleThemeChange(
                item.value
              )
            }
            className={`
              group
              flex
              flex-col
              items-center
              justify-center
              gap-2
              rounded-xl
              border
              px-3
              py-3
              transition-all
              duration-200

              ${
                isActive
                  ? `
                    border-primary/30
                    bg-primary/10
                    text-primary
                    shadow-[0_0_20px_rgba(34,197,94,0.08)]
                  `
                  : `
                    border-white/[0.08]
                    bg-white/[0.025]
                    text-muted-foreground
                    hover:border-white/[0.14]
                    hover:bg-white/[0.05]
                    hover:text-foreground
                  `
              }
            `}
          >
            <Icon
              className="
                h-4
                w-4
                transition-transform
                duration-200
                group-hover:scale-110
              "
            />

            <span className="text-[11px] font-medium">
              {item.label}
            </span>
          </button>
        );
      })}
    </div>
  );
}