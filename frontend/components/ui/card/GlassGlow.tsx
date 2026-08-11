export default function GlassGlow() {
  return (
    <div
      className="
        pointer-events-none
        absolute
        inset-0
        rounded-3xl
        bg-gradient-to-br
        from-primary/10
        via-transparent
        to-primary/5
        opacity-0
        blur-3xl
        transition-opacity
        duration-500
        group-hover:opacity-100
      "
    />
  );
}