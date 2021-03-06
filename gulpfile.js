'use strict';

var autoprefixer = require('gulp-autoprefixer');
var browserSync = require('browser-sync').create();
var concat = require('gulp-concat');
var exec = require('child_process').exec;
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
    py: '**/*.py',
    sass: appName + '/sass/**/*.scss',
    templates: '**/templates/**/*.html',
};
var port = gutil.env.port ? gutil.env.port : '8000'
var uiPort = gutil.env.ui ? gutil.env.ui : '3000'

gulp.task('browserSyncInit', function() {
    browserSync.init({
        logPrefix: 'Browsersync:' + appName,
        port: port,
        proxy: '127.0.0.1:' + port,
        ui: { port: uiPort },
    });
});

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

gulp.task('runserver', function() {
    var proc = exec('PYTHONUNBUFFERED=1 python manage.py runserver ' + port,
        function (error) {
            if (error !== null) {
              throw Error(gutil.colors.magenta(
                'Runserver Error -- is port already in use?'));
            }
        }
    );

    proc.stderr.on('data', function(data) {
        process.stderr.write(data);
    });

    proc.stdout.on('data', function(data) {
        process.stdout.write(data);
    });
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

gulp.task('watch', ['browserSyncInit'], function() {
    gulp.watch(paths.sass, ['sass']);
    gulp.watch(paths.js + '/app/**/*.js', ['js_app']);
    gulp.watch(paths.js + '/vendor/**/*.js', ['js_vendor']);
    gulp.watch([paths.py, paths.templates]).on('change', function(){
        runSequence('touchPy', 'reloadBrowsers');
    });
});

gulp.task('default', ['js_app', 'js_vendor', 'sass', 'runserver', 'watch']);
