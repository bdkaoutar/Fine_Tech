import { APP_BASE_HREF } from '@angular/common';
import { CommonEngine } from '@angular/ssr';
import express from 'express';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';
import bootstrap from './src/main.server';

// Function to initialize the Express server
export function app(): express.Express {
  const server = express();

  // Directories for server-side rendering
  const serverDistFolder = dirname(fileURLToPath(import.meta.url));
  const browserDistFolder = resolve(serverDistFolder, '../browser');
  const indexHtml = join(serverDistFolder, 'index.server.html');

  const commonEngine = new CommonEngine();

  // Set view engine
  server.set('view engine', 'html');
  server.set('views', browserDistFolder);

  // Serve static files from the browser build
  server.get('*.*', express.static(browserDistFolder, { maxAge: '1y' }));

  // Handle all other routes with the Angular engine
  server.get('*', (req, res, next) => {
    try {
      const { protocol, originalUrl, baseUrl, headers } = req;

      // Render the application using CommonEngine
      commonEngine
        .render({
          bootstrap,
          documentFilePath: indexHtml,
          url: `${protocol}://${headers.host}${originalUrl}`,
          publicPath: browserDistFolder,
          providers: [
            {
              provide: APP_BASE_HREF,
              useValue: baseUrl || '/',
            },
          ],
        })
        .then((html) => {
          res.send(html);
        })
        .catch((err) => {
          console.error('Error rendering Angular application:', err);
          next(err);
        });
    } catch (err) {
      console.error('Critical server error:', err);
      next(err);
    }
  });

  return server;
}

// Function to start the server
function run(): void {
  const port = process.env['PORT'] || 4000;

  // Start up the Node server
  const server = app();
  server.listen(port, () => {
    console.log(`Node Express server is listening on http://localhost:${port}`);
  });
}

run();
