# 11x Web App

## Service Description and Philosophy
This is a React application scaffolded and supported by Vite, with Shadcn + TailwindCSS for a component library, and Vitest with React Testing Libary for unit testing.

## Usage Instructions
Clone the repo, `cd` into it then...

`npm install`

`npm run dev`

...to start up the dev server on port 5173

Utility scripts:

`npm run lint` to run eslint

`npm run prettier:check` to check formatting

`npm run prettier:format` to format

`npm run test` to run unit tests

See package.json for more details


## Proposed Next Steps:
- Fix a few implicit any types
- Finish Dockerizing and composing
- Add Github Actions for linting, testing, building, deployment
- Identify further abstraction candidates
- Additional error handling
- Additional features
  - ~~Silhouette scores and number of clusters determination~~
  - Clustering visualization 
  - Interesting variant flags
- Auth
