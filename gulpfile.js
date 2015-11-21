'use strict';

var autoprefixer = require('gulp-autoprefixer');
var browserSync = require('browser-sync').create();
var concat = require('gulp-concat');
var gulp = require('gulp');
var gutil = require('gulp-util');
var runSequence = require('run-sequence');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var wait = require('gulp-wait');

var appName = 'cms_lab_publications';
var paths = {
    css: appName + '/static/' + appName + '/css',
    js: appName + '/static/' + appName + '/js',
    sass: appName + '/sass/app.scss',
    templates: '**/templates/**/*.html',
};

gulp.task('js_app', function() {
    browserSync.notify('Compiling App JavaScript');
    return gulp.src(paths.js + '/app/**/*.js')
        .pipe(sourcemaps.init())
            .pipe(concat('app.js'))
            .pipe(uglify())
        .pipe(sourcemaps.write('../maps'))
        .pipe(gulp.dest(paths.js))
        .pipe(browserSync.stream());
});

gulp.task('js_vendor', function() {
    browserSync.notify('Compiling Vendor JavaScript');
    return gulp.src(paths.js + '/vendor/**/*.js')
        .pipe(sourcemaps.init())
            .pipe(concat('vendor.js'))
            .pipe(uglify())
        .pipe(sourcemaps.write('../maps'))
        .pipe(gulp.dest(paths.js))
        .pipe(browserSync.stream());
});

gulp.task('reloadBrowsers', function() {
    browserSync.notify('Reloading Browsers');
    browserSync.reload();
});

gulp.task('sass', function() {
    browserSync.notify('Compiling Sass');
    return gulp.src(paths.sass)
        .pipe(sourcemaps.init())
            .pipe(sass({ outputStyle: 'compressed' }))
            .pipe(autoprefixer())
        .pipe(sourcemaps.write('../maps'))
        .pipe(gulp.dest(paths.css))
        .pipe(browserSync.stream());
});

gulp.task('touchPy', function() {
    // Touch a .py file in order to trigger runserver to restart
    // and then wait a moment while it restarts.
    browserSync.notify('Restarting Runserver');
    return gulp.src(appName + '/__init__.py')
        .pipe(gulp.dest(appName))
        .pipe(wait(2000));
});

gulp.task('watch', function() {
    browserSync.init({
        port: gutil.env.port ? gutil.env.port : '8000',
        proxy: '127.0.0.1:8000',
        ui: { port: gutil.env.ui ? gutil.env.ui : '8001' },
    });
    gulp.watch(paths.sass, ['sass']);
    gulp.watch(paths.js + '/app/**/*.js', ['js_app']);
    gulp.watch(paths.js + '/vendor/**/*.js', ['js_vendor']);
    gulp.watch(paths.templates).on('change', function(){
        runSequence('touchPy', 'reloadBrowsers');
    });
});

gulp.task('default', ['js_app', 'js_vendor', 'sass', 'watch']);
