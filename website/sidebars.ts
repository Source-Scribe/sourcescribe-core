import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'api-reference/README',
      label: 'Documentation Home',
    },
    {
      type: 'category',
      label: 'Overview',
      collapsed: false,
      items: [
        'api-reference/overview/index',
        'api-reference/overview/architecture',
        'api-reference/overview/technology-stack',
      ],
    },
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'api-reference/getting-started/installation',
        'api-reference/getting-started/quick-start',
        'api-reference/getting-started/configuration',
      ],
    },
    {
      type: 'category',
      label: 'Features',
      items: [
        'api-reference/features/index',
      ],
    },
    {
      type: 'category',
      label: 'Architecture',
      items: [
        'api-reference/architecture/components',
      ],
    },
  ],
};

export default sidebars;
