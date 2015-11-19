'use strict';

var autoprefixer = require('gulp-autoprefixer');
var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');

var paths = {
    css: 'cms_lab_publications/static/cms_lab_publications/css',
    sass: 'cms_lab_publications/sass/app.scss',
}

gulp.task('sass', function() {
    gulp.src(paths.sass)
        .pipe(sourcemaps.init())
            .pipe(sass({ outputStyle: 'compressed' }))
            .pipe(autoprefixer())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(paths.css));
});

gulp.task('watch', function() {
    gulp.watch(paths.sass, ['sass']);
});

gulp.task('default', ['sass', 'watch']);
