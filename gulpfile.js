'use strict';

var browserify = require('browserify');
var gulp = require('gulp');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');

var less = require('gulp-less');
var plumber = require('gulp-plumber');
var watch = require('gulp-watch');
var path = require('path')
var gutil = require('gulp-util');
var watchify = require('watchify');
var livereload = require('gulp-livereload');
var srcDir = './static/src'
var buildDir = './static/build'


var paths = {
  less: {
    src: srcDir + '/less/*.less',
    main: srcDir + '/less/styles.less',
    dest: buildDir + '/css'
  },
  js: {
    src: srcDir + '/js/**',
    main: srcDir + '/js/main.js',
    dest: buildDir + '/js'
  }
}


gulp.task('lessWatch', function() {
  return gulp.src(paths.less.main)
    .pipe(plumber())
    .pipe(watch())
    .pipe(less())
    .pipe(gulp.dest(paths.less.dest));
});

gulp.task('less', function() {
  // Recompile main upon any less file change.
  return gulp.src(paths.less.main)
    .pipe(less())
    .pipe(gulp.dest(paths.less.dest));
});

gulp.task('browserify-watch', function(){
  browserifyBundle();
});


function browserifyBundle() {
  var b = browserify(paths.js.main, {
    cache: {},
    packageCache: {},
    fullPaths: true,
    debug: true
  });

  b = watchify(b);
  b.on('update', function(){
    rebundle(b);
  });

  rebundle(b)
}

function rebundle(b){
  b.bundle()
  .pipe(source('bundle.js'))
  .pipe(buffer())
  .pipe(sourcemaps.init({loadMaps: true}))
    // Add transformation tasks to the pipeline here.
  .pipe(uglify())
  .pipe(sourcemaps.write('./'))
  .pipe(gulp.dest(paths.js.dest));
}

gulp.task('watch', ['browserify-watch'], function() {
  gulp.watch(paths.less.main, ['lessWatch']);
});
