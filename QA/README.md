<<<<<<< HEAD
# QA

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 16.2.7.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
=======

# README.md

Ensure you have the necessary environment and tools installed. If you have the provided environment, activate it to avoid installing packages globally.

## Backend Installation

```sh
git clone https://github.com/Ghk21nznz21/Q-A.git
```

### Backend-Flask:

Navigate to the backend directory:

```sh
cd backend
```

If you have the provided environment, activate it:

```sh
source qaenv/bin/activate  # On Linux/macOS
qaenv\Scripts\activate     # On Windows
```

Then, install the necessary packages:

```sh
pip install flask
pip install flask-cors
```

Run the Flask application:

```sh
python -m Flask
```

### Frontend-Angular:

Navigate to the frontend directory:

```sh
cd frontend
```

If you have the provided environment, activate it:

```sh
source qaenv/bin/activate  # On Linux/macOS
qaenv\Scripts\activate     # On Windows
```

Install the necessary packages:

```sh
npm install -g @angular/cli
npm install
npm install tailwindcss
npm install flowbite
npm install @angular/core @angular/router @angular/common @angular/platform-browser @angular/platform-browser-dynamic
```

**Note**: If you encounter an issue related to the mismatch version between `typescript` and `@angular/compiler-cli`, adjust the `typescript` version:

```sh
npm uninstall typescript
npm install typescript@4.9.3
```

Then, install the required Angular devkit:

```sh
npm install --save-dev @angular-devkit/build-angular
```

Finally, serve the application:

```sh
ng serve --open
```

---

## Alterations Made:

1. **Installed Missing Angular Modules**: Added `@angular/router`, `@angular/common`, `@angular/platform-browser`, and `@angular/platform-browser-dynamic`.
2. **TypeScript Version Adjustment**: Changed the `typescript` version to `4.9.3` to ensure compatibility with `@angular/compiler-cli`.
3. **Angular Devkit Installation**: Added `@angular-devkit/build-angular` for Angular build specific commands.
4. **TypeScript Configuration**: Updated `tsconfig.json` to enable `experimentalDecorators`.
5. **Type Annotations**: Modified `app.component.ts` to add explicit types to parameters, resolving implicit 'any' type errors.
>>>>>>> origin/main
