'use strict';

var autoprefixer = require('gulp-autoprefixer');
var concat = require('gulp-concat');
var gulp = require('gulp');
var livereload = require('gulp-livereload');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');

var appName = 'cms_lab_publications';
var paths = {
    css: appName + '/static/' + appName + '/css',
    js: appName + '/static/' + appName + '/js',
    sass: appName + '/sass/app.scss',
    templates: '**/templates/**/*.html',
};

gulp.task('js_app', function() {
    return gulp.src(paths.js + '/app/**/*.js')
        .pipe(sourcemaps.init())
            .pipe(concat('app.js'))
            .pipe(uglify())
        .pipe(sourcemaps.write('../maps'))
        .pipe(gulp.dest(paths.js))
        .pipe(livereload());
});

gulp.task('js_vendor', function() {
    return gulp.src(paths.js + '/vendor/**/*.js')
        .pipe(sourcemaps.init())
            .pipe(concat('vendor.js'))
            .pipe(uglify())
        .pipe(sourcemaps.write('../maps'))
        .pipe(gulp.dest(paths.js))
        .pipe(livereload());
});

gulp.task('sass', function() {
    return gulp.src(paths.sass)
        .pipe(sourcemaps.init())
            .pipe(sass({ outputStyle: 'compressed' }))
            .pipe(autoprefixer())
        .pipe(sourcemaps.write('../maps'))
        .pipe(gulp.dest(paths.css))
        .pipe(livereload());
});

function touchPy() {
    gulp.src(appName + '/__init__.py')
        .pipe(gulp.dest(appName));
}

gulp.task('watch', function() {
    livereload.listen();
    gulp.watch(paths.sass, ['sass']);
    gulp.watch(paths.js + '/app/**/*.js', ['js_app']);
    gulp.watch(paths.js + '/vendor/**/*.js', ['js_vendor']);
    gulp.watch(paths.templates).on('change', function(file) {
        touchPy();
        livereload.changed(file);
    });
});

gulp.task('default', ['js_app', 'js_vendor', 'sass', 'watch']);
