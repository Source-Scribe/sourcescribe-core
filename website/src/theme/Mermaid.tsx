import React, { useEffect, useRef } from 'react';
import Mermaid from '@theme-original/Mermaid';
import type MermaidType from '@theme/Mermaid';
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof MermaidType>;

export default function MermaidWrapper(props: Props): React.ReactElement {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Add zoom controls after diagram renders
    const container = containerRef.current;
    if (!container) return;

    const svg = container.querySelector('svg');
    if (!svg) return;

    // Add click-to-zoom functionality
    let scale = 1;
    const handleWheel = (e: WheelEvent) => {
      e.preventDefault();
      const delta = e.deltaY > 0 ? 0.9 : 1.1;
      scale *= delta;
      scale = Math.max(0.5, Math.min(scale, 3)); // Limit zoom range
      svg.style.transform = `scale(${scale})`;
    };

    // Enable mouse wheel zoom
    container.addEventListener('wheel', handleWheel, { passive: false });

    return () => {
      container.removeEventListener('wheel', handleWheel);
    };
  }, []);

  return (
    <div ref={containerRef} className="mermaid-zoom-container">
      <Mermaid {...props} />
      <div className="mermaid-controls">
        <small style={{ opacity: 0.7, fontSize: '11px' }}>
          Use mouse wheel to zoom • Click and drag to pan
        </small>
      </div>
    </div>
  );
}
