// Import with `import * as Sentry from "@sentry/node"` if you are using ESM
import * as Sentry from '@sentry/bun';

Sentry.init({
  dsn: 'https://c9833f17324faaa8d74b8ef35ed87798@o4504376009687040.ingest.us.sentry.io/4507864794005504',
  integrations: [],
  // Tracing
  tracesSampleRate: 1.0, //  Capture 100% of the transactions

  // Set `tracePropagationTargets` to control for which URLs trace propagation should be enabled
  tracePropagationTargets: ['localhost', /^https:\/\/yourserver\.io\/api/],
});
