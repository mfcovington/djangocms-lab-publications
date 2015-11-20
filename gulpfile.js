'use strict';

var autoprefixer = require('gulp-autoprefixer');
var gulp = require('gulp');
var livereload = require('gulp-livereload');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');

var appName = 'cms_lab_publications';
var paths = {
    css: appName + '/static/' + appName + '/css',
    sass: appName + '/sass/app.scss',
    templates: '**/templates/**/*.html',
};

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
    gulp.watch(paths.templates).on('change', function(file) {
        touchPy();
        livereload.changed(file);
    });
});

gulp.task('default', ['sass', 'watch']);
